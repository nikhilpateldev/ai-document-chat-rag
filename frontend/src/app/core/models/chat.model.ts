import { SourceReference } from './source.model';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  confidence?: number;
  sources?: SourceReference[];
}

export type SSEEvent =
  | { type: 'token'; content: string }
  | { type: 'sources'; sources: SourceReference[] }
  | { type: 'confidence'; value: number }
  | { type: 'done' };
