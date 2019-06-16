import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { FreelyUser } from '../../models/freely-user'
import { FileChooser } from '@ionic-native/file-chooser';
import { Base64 } from '@ionic-native/base64/ngx';


@Component({
  selector: 'page-user-details',
  templateUrl: 'user-details.html',
})
export class UserDetailsPage {
  picturePath: any = "assets/imgs/profile.jpg";
  
  userName: string = "Lorina Dundau";
  description: string = "Lorem ipsum dolor sit amet";
  email: string = "lorina.dundau@gmail.com";
  phone: string = "0745048848";
  rating: string = "4.3";
  userData: FreelyUser = {
    firstName:" ",
    lastName:" ",
    description:" ",
    email: " ",
    rating: " ",
    birthdate: " "
  };

  constructor(private base64: Base64, private fileChooser: FileChooser, public navCtrl: NavController, public navParams: NavParams) {

  }

  ionViewDidLoad() {
    try {
      if(localStorage.getItem("userData")) {
        this.userData = JSON.parse(localStorage.getItem("userData"))
      }
  } catch (error) {
      
  }
    console.log('ionViewDidLoad UserDetailsPage');
  }

  editImage() {
    this.fileChooser.open()
    .then(uri => {
      this.base64.encodeFile(uri).then((base64File: string) => {
        console.log(base64File);
        this.picturePath = uri;
        alert(base64File);
      }, (err) => {
        console.log("## LOOK HERE");
        console.log(err);
      });
    });
  }


  onEdit(){

  }

}
