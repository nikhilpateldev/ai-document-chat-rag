import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { SSEEvent } from '../models/chat.model';

@Injectable({ providedIn: 'root' })
export class SseService {

  async streamChat(
    payload: unknown,
    onEvent: (e: SSEEvent) => void,
    signal?: AbortSignal
  ): Promise<void> {

    const res = await fetch(`${environment.apiBaseUrl}/chat/ask-stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify(payload),
      signal
    });

    if (!res.ok) {
      throw new Error(`SSE request failed: ${res.status}`);
    }

    if (!res.body) {
      throw new Error('Streaming not supported by browser');
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        if (!value) continue; // ✅ critical safety

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data:')) continue;

          try {
            const json = trimmed.replace(/^data:\s*/, '');
            const event = JSON.parse(json) as SSEEvent;
            onEvent(event);
          } catch (err) {
            console.warn('Invalid SSE payload:', trimmed);
          }
        }
      }
    } catch (err: any) {
      // 🔴 Abort is NOT an error – expected behavior
      if (err?.name !== 'AbortError') {
        console.error('SSE stream error:', err);
        throw err;
      }
    } finally {
      reader.releaseLock();
    }
  }
}
