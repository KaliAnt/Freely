import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { FreelyOrganization } from '../../models/freely-organization'

/**
 * Generated class for the OrganizationDetailsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-organization-details',
  templateUrl: 'organization-details.html',
})
export class OrganizationDetailsPage {

  organization: FreelyOrganization = {
    name: " ",
    email: " ",
    description: " ",
    rating: "5.0"
  }

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    try {
      if(localStorage.getItem("userData")) {
        this.organization = JSON.parse(localStorage.getItem("userData"))
      }
  } catch (error) {
      
  }
    console.log('ionViewDidLoad OrganizationDetailsPage');
  }

}
