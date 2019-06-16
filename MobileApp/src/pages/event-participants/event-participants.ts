import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { UserApplicationProvider } from '../../providers/user-application/user-application'
import { FreelyUserApplication } from '../../models/freely-user-application'

/**
 * Generated class for the EventParticipantsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-event-participants',
  templateUrl: 'event-participants.html',
})
export class EventParticipantsPage {

  private event = this.navParams.data;
  private eventName: string;

  private applicationList: Array<FreelyUserApplication>;
  
  constructor(private userApplicationProvider: UserApplicationProvider, public navCtrl: NavController, public navParams: NavParams) {

  }

  ionViewDidLoad() {
    this.eventName = this.event.name;
    this.getUsersForEvent();
    console.log('ionViewDidLoad EventParticipantsPage');
  }

  getUsersForEvent() {
    console.log("EVENT NAME:");
    console.log(this.eventName);
    this.userApplicationProvider.getUsersForEvent(this.eventName, "*").then(result => {
      if(result.status == "OK") {
        try {
            console.log("APPLICATIONS req:");
            console.log(result.users);
            this.applicationList = result.users;
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

  acceptUser(item){
    this.userApplicationProvider.modifyStatusForApplication(this.eventName, item.email, "Accepted").then(result => {
      if(result.status == "OK") {
        item.appStatus = "Accepted";
      }
      else{
        console.log("Invalid application data!");
      }
    });
  }

  viewUser(item){
  }
  rejectUser(item){
    this.userApplicationProvider.modifyStatusForApplication(this.eventName, item.email, "Rejected").then(result => {
      if(result.status == "OK") {
        item.appStatus = "Rejected";
      }
      else{
        console.log("Invalid application data!");
      }
    });

  }

  getItemColor(item){
    if(item.appStatus == "Pending"){
      return "white";
    }
    if(item.appStatus == "Rejected"){
      return "third";
    }else{
      return "secondary";
    }
  }

}
