import { Component, signal } from '@angular/core';
import { ChatMessage, SSEEvent } from '../../core/models/chat.model';
import { SseService } from '../../core/services/sse.service';
import { ChatSessionService } from '../../core/services/chat-session.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat',
  standalone: true,
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
  imports: [CommonModule]
})
export class ChatComponent {
  messages = signal<ChatMessage[]>([]);
  loading = signal(false);

  private abortController?: AbortController;

  constructor(
    private sse: SseService,
    private session: ChatSessionService
  ) {}

  ask(question: string): void {
    if (!question.trim()) return;

    // 🔴 Abort previous stream if running
    this.abortController?.abort();
    this.abortController = new AbortController();

    const user: ChatMessage = {
      role: 'user',
      content: question
    };

    const ai: ChatMessage = {
      role: 'assistant',
      content: ''
    };

    this.messages.update(m => [...m, user, ai]);
    this.loading.set(true);

    this.sse.streamChat(
      {
        sessionId: this.session.sessionId(),
        question
      },
      (event: SSEEvent) => {
        this.messages.update(messages => {
          const updated = [...messages];
          const last = { ...updated[updated.length - 1] };

          if (event.type === 'token') {
            last.content += event.content;
          }

          if (event.type === 'sources') {
            last.sources = event.sources;
          }

          if (event.type === 'confidence') {
            last.confidence = event.value;
          }

          updated[updated.length - 1] = last;
          return updated;
        });

        if (event.type === 'done') {
          this.loading.set(false);
        }
      },
      this.abortController.signal
    ).catch(() => {
      // 🟡 Always reset loading on failure
      this.loading.set(false);
    });
  }
}

