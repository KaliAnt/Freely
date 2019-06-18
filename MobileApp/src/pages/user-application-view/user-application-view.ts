import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { UserApplicationProvider } from '../../providers/user-application/user-application';
import { FreelyOrganization } from '../../models/freely-organization';
import { FreelyEventData } from '../../models/freely-event-data';
import { FreelyEventApplicationView } from '../../models/freely-event-application-view';
import { EventDetailsViewPage } from '../event-details-view/event-details-view';
import { FreelyEvent } from '../../models/freely-event';
import { FeedbackProvider } from '../../providers/feedback/feedback'
import { FeedbackFormPage } from '../feedback-form/feedback-form';

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
  private canGiveFeedbacks : Array<any>;


  constructor(private feedbackProvider:FeedbackProvider, private userApplicationProvider: UserApplicationProvider, public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    this.getUserApplications();
    console.log('ionViewDidLoad UserApplicationViewPage');
  }

  getUserApplications() {
    var user = JSON.parse(localStorage.getItem("userData"));
    console.log("USER EMAIL:");
    console.log(user.email);
    this.userApplicationProvider.getUserApplications(user.email).then(result => {
      if(result.status == "OK") {
        try {
            
            this.applicationList = result.applications;
            for (let entry of this.applicationList) 
              this.feedbackProvider.canGiveFeedback(entry.event.name).then(result => {
                 if(result.status == "OK")
                  console.log("OK");
                 
              });

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

  getFeedbackButton(item) {
    // return false;
    
    return true;
  }

  giveFeedback(item) {
    console.log("THIS IS BEFORE PUSH:")
    console.log(item.event)
    this.navCtrl.push(FeedbackFormPage,{event:item.event});
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
