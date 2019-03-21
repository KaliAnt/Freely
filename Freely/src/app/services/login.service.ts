import { Injectable } from '@angular/core';
import { RequestService } from './request.service';
import { EmailValidator } from '@angular/forms';
import 'rxjs/add/operator/map';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(private requestProvider: RequestService) {
    console.log('LoginService');
   }

   login(email: string, password: string): Promise<any> {
     var payload = {
       email: email,
       password: password
     }
     return this.requestProvider.buildPost("login", payload, false).map(data => data.json()).toPromise();
   }
   
}