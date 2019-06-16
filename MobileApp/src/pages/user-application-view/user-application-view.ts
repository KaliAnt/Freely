import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { UserApplicationProvider } from '../../providers/user-application/user-application';
import { FreelyOrganization } from '../../models/freely-organization';
import { FreelyEventData } from '../../models/freely-event-data';
import { FreelyEventApplicationView } from '../../models/freely-event-application-view';
import { EventDetailsViewPage } from '../event-details-view/event-details-view';
import { FreelyEvent } from '../../models/freely-event';

/**
 * Generated class for the UserApplicationViewPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */


@Component({
  selector: 'page-user-application-view',
  templateUrl: 'user-application-view.html',
})
export class UserApplicationViewPage {
  private applicationList: Array<FreelyEventApplicationView>;


  constructor(private userApplicationProvider: UserApplicationProvider, public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    this.getUsersForEvent();
    console.log('ionViewDidLoad UserApplicationViewPage');
  }

  getUsersForEvent() {
    var user = JSON.parse(localStorage.getItem("userData"));
    console.log("USER EMAIL:");
    console.log(user.email);
    this.userApplicationProvider.getUserApplications(user.email).then(result => {
      if(result.status == "OK") {
        try {
            console.log("APPLICATIONS req:");
            console.log(result.applications);
            this.applicationList = result.applications;
            console.log("APPLICATIONS:");
            console.log(this.applicationList);
          } catch (error) {
            console.log("invalid applications list");
          }
        }
      else{
        console.log("Invalid event data!");
      }
    });
  }

  getItemColor(item){
    if(item.appStatus == "Pending"){
      return "primary";
    }
    if(item.appStatus == "Rejected"){
      return "third";
    }else{
      return "secondary";
    }
  }

  viewEvent(item) {
    var event: FreelyEvent = {
      name : item.event.name,
      date : item.event.date,
      location : item.event.location,
      description : item.event.description,
      organizer : item.event.organization.name,
      organizerEmail : item.event.organization.email
    }

    this.navCtrl.push(EventDetailsViewPage,{item:event});
  }
}
