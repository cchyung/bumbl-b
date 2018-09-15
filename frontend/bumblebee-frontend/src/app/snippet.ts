import {Audio} from './audio';

export class Snippet {
  audio: Audio;
  start: number;
  end: number;
  url: string;
}

export class SnippetListItem {
  word: string;
  snippet: Snippet;
}
