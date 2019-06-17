import { Injectable } from '@angular/core';
import { RequestProvider } from '../request/request';


@Injectable()
export class FileProvider {

  constructor(private requestProvider: RequestProvider) {
    console.log('Hello FileProvider Provider');
  }

  sendCVFile(fileBlob: any, email: string): Promise<any>{
    var payload ={
      type: "cv",
      extension: "pdf",
      email: email,
      file: fileBlob
    }
    return this.requestProvider.buildPost("uploadFile", payload, false).map(data => data.json()).toPromise();
  }

}
