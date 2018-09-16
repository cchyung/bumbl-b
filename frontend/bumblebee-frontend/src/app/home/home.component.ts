import { Component, OnInit } from '@angular/core';
import {HttpService} from '../http.service';
import {Snippet, SnippetListItem} from '../snippet';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  state = 0;
  snippets: SnippetListItem[];
  newSnippets: Snippet[];  // contains the new snippets if user wants to replace a word

  /*
    State explanation:
    0: main screen
    1: loading spinner
    2: display sentence and play button
    3: display alternatives
   */

  constructor(private httpService: HttpService) { }

  ngOnInit() {
    this.state = 0;
  }

  processSentence(sentence: string): void {
    this.httpService.processSentence(sentence).subscribe(
      snippets => {
        this.snippets = snippets;
        this.state = 2;
      }
    );
    this.state = 1;
  }

  playSentence(): void {
    // Plays each audio file
  }

  getNewSnippets(word: string): void {
    this.httpService.getSnippets(word).subscribe(
      snippets => {
        this.newSnippets = snippets;
        this.state = 3;
      }
    );
    this.state = 1; // show small loading spinner
  }
}
