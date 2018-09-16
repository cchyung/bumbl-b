import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Snippet, SnippetListItem} from './snippet';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private baseUrl = 'api';

  constructor(private http: HttpClient) { }

  processSentence(sentence: string): Observable<SnippetListItem[]> {
    const url = `${this.baseUrl}/process-sentence`;
    return this.http.get<SnippetListItem[]>(url, {params: {query: sentence}});
  }

  getSnippets(word: string): Observable<Snippet[]> {
    const url = `${this.baseUrl}/get-snippets`;
    const params: HttpParams = new HttpParams();
    params.append('query', word);
    return this.http.get<Snippet[]>(url, {params: params});
  }
}
