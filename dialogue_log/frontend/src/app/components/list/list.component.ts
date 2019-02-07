import { Conversation } from './../../conversation.model';
import { ConversationService } from './../../conversation.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  conversations: Conversation[];
  displayedColumns = ['sender_id', 'actions'];

  constructor(private conversationService: ConversationService) { }
  ngOnInit() {
    this.fetchConversations();
  }

  fetchConversations() {
    this.conversationService
      .getConversations()

      .subscribe((data: Conversation[]) => {
        this.conversations = data;
        console.log('Requesting conversations ... ');
        console.log(this.conversations);

      });
  }

  deleteConversation(id) {
    this.conversationService.deleteConversations(id).subscribe(() => {
      this.fetchConversations();
    });
  }
}