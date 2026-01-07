import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class DocumentService {
  async upload(file: File): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
      `${environment.apiBaseUrl}/documents/upload`,
      { method: 'POST', body: formData }
    );

    if (!response.ok) {
      throw new Error('Upload failed');
    }
  }
}
