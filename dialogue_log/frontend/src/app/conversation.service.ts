import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class ConversationService {
  uri = 'http://localhost:4221';
  constructor(private http: HttpClient) {
  }

  getConversations() {
    return this.http.get(`${this.uri}/conversations`);
  }
  deleteConversations(id) {
    return this.http.get(`${this.uri}/conversations/delete/${id}`);
  }
}
