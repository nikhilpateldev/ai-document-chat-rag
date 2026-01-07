import { Routes } from '@angular/router';
import { ChatComponent } from './features/chat/chat.component';
import { DocumentUploadComponent } from './features/upload/document-upload.component';

export const routes: Routes = [
  { path: '', redirectTo: 'chat', pathMatch: 'full' },
  { path: 'chat', component: ChatComponent },
  { path: 'upload', component: DocumentUploadComponent }
];