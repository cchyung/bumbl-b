import { Component, OnInit } from '@angular/core';
declare var $: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'bumblebee-frontend';

  ngOnInit() {
    $(window).resize(function () {
      this.resizeDiv();
    });

    this.resizeDiv();
  }

  resizeDiv() {
    const vph = $(window).height();
    if (vph > 500) {
      $('.auto-resize').css({'height': vph + 'px'});
    }
  }
}
