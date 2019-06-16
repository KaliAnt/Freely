import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { FreelyUserApplication } from '../../models/freely-user-application'

/**
 * Generated class for the UserPublicProfilePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-user-public-profile',
  templateUrl: 'user-public-profile.html',
})
export class UserPublicProfilePage {
  private user : FreelyUserApplication = {
    firstName: "",
    lastName: "",
    email: "",
    rating: "",
    birthdate: "",
    description: "",
    appStatus: ""
  }
  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.user = navParams.get('item');
  }

  ionViewDidLoad() {

    console.log('ionViewDidLoad UserPublicProfilePage');
  }

}
