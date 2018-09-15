import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Snippet} from './snippet';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private baseUrl = 'api/';

  constructor(private http: HttpClient) { }

  processSentence(sentence: string): Observable<Snippet[]> {
    const url = `${this.baseUrl}/process-sentence`;
    const params: HttpParams = new HttpParams();
    params.append('query', sentence);
    return this.http.get<Snippet[]>(url, {params: params});
  }

  getSnippets(word: string): Observable<Snippet[]> {
    const url = `${this.baseUrl}/get-snippets`;
    const params: HttpParams = new HttpParams();
    params.append('query', word);
    return this.http.get<Snippet[]>(url, {params: params});
  }
}
