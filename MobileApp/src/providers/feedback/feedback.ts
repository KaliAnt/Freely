import { Injectable } from '@angular/core';
import { RequestProvider } from '../request/request';


/*
  Generated class for the FeedbackProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class FeedbackProvider {

  canGiveFeedback(event: string) {
    var payload = {
      event: event
    }
    return this.requestProvider.buildPost("canGiveFeedback", payload, false).map(data => data.json()).toPromise();
  }

  postFeedback(email: string, type:string, rating: string, description: string) {
    var payload = {
      email: email,
      forThis: type,
      rating: rating,
      description: description
    }
    return this.requestProvider.buildPost("postFeedback", payload, false).map(data => data.json()).toPromise();
  }
  
  constructor(private requestProvider: RequestProvider) {
    console.log('Hello FeedbackProvider Provider');
  }

}
