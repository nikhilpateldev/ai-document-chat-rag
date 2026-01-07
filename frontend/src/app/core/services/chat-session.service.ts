import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ChatSessionService {
  readonly sessionId = signal(crypto.randomUUID());
  reset() {
    this.sessionId.set(crypto.randomUUID());
  }
}
