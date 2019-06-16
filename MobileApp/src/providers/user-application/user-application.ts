import { RequestProvider } from '../request/request';
import { Injectable } from '@angular/core';

/*
  Generated class for the UserApplicationProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class UserApplicationProvider {

  constructor(private requestProvider: RequestProvider) {
    console.log('Hello UserApplicationProvider Provider');
  }

  getUsersForEvent(name: string, status: string) {
    var payload = {
      name: name,
      status: status
    }
    return this.requestProvider.buildPost("getUsersForEvent", payload, false).map(data => data.json()).toPromise();
  }

  modifyStatusForApplication(event: string, email: string, status: string) {
    var payload = {
      event: event,
      email: email,
      status: status
    }
    return this.requestProvider.buildPost("modifyStatusForApplication", payload, false).map(data => data.json()).toPromise();
  }

}
