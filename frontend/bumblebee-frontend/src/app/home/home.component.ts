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
  wordToReplace = 0;
  snippets: SnippetListItem[];
  newSnippets: Snippet[];  // contains the new snippets if user wants to replace a word
  audioFiles = [];

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
        console.log(snippets);
        this.loadAudio();
      }
    );
    this.state = 1;
  }

  loadAudio(): void {
    for (const snippet of this.snippets) {
      const audio = new Audio();
      if (snippet.snippet) {
        audio.src = snippet.snippet.url;
        audio.load(); // load audio file and push
        this.audioFiles.push(audio);
        console.log(this.audioFiles);
      }
    }
    this.state = 2;
  }

  playSentence(): void {
    console.log('playSentence()');
    this.playWord(0);
  }

  playWord(index: number): void {
    if (index === this.audioFiles.length) {
      return;
    } else {
      const audio = this.audioFiles[index];
      audio.play();
      setTimeout(() => {
        this.playWord(index + 1);
      },  audio.duration * 900);
    }
  }

  startOver(): void {
    this.state = 0;
    this.audioFiles = [];
    this.newSnippets = [];
    this.snippets = [];
  }

  getNewSnippets(index: number, word: string): void {
    this.state = 1; // show small loading spinner
    this.wordToReplace = index;
    this.httpService.getSnippets(word).subscribe(
      snippets => {
        this.newSnippets = snippets;
        this.state = 3;
      }
    );
  }

  updateSnippet(index: number): void {
    console.log(`updating word ${this.wordToReplace} : ${this.snippets[this.wordToReplace].word} to ${this.newSnippets[index].audio.name}`);
    this.snippets[this.wordToReplace] = new SnippetListItem(this.snippets[this.wordToReplace].word, this.newSnippets[index]);
    this.state = 2;
    this.audioFiles = []
    this.loadAudio();
  }

  closeAlternatives(): void {
    this.state = 2;
  }

}
