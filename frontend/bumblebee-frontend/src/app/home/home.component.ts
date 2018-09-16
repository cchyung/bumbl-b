import { Component, OnInit } from '@angular/core';
import {HttpService} from '../http.service';
import {SnippetListItem} from '../snippet';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  state = 0;
  snippets: SnippetListItem[];

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
}
