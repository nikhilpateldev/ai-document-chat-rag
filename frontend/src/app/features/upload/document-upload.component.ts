import { Component, signal } from '@angular/core';
import { environment } from '../../../environments/environment';
import { DocumentService } from '../../core/services/document.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  templateUrl: './document-upload.component.html',
  styleUrls: ['./document-upload.component.css']
})
export class DocumentUploadComponent {
  status = signal('');
  constructor(private documentService: DocumentService) {

  }
  async onFileSelected(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {
      return;
    }

    const file = input.files[0];

    this.status.set('Uploading...');
    try {
      await this.documentService.upload(file);
      this.status.set('Upload successful');
    } catch {
      this.status.set('Upload failed');
    }
  }
}
