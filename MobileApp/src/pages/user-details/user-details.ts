import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { FreelyUser } from '../../models/freely-user'

@Component({
  selector: 'page-user-details',
  templateUrl: 'user-details.html',
})
export class UserDetailsPage {

  
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

  constructor(public navCtrl: NavController, public navParams: NavParams) {

  }

  ionViewDidLoad() {
    try {
      if(localStorage.getItem("userData")) {
        this.userData = JSON.parse(localStorage.getItem("userData"))
        console.log("THIS IS THE DATA");
        console.log(this.userData);   
      }
  } catch (error) {
      
  }
    console.log('ionViewDidLoad UserDetailsPage');
  }

  onEdit(){

  }

}
