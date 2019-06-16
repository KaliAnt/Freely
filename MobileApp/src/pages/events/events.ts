import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { CreateEventPage } from '../../pages/create-event/create-event';
import { ModalController } from 'ionic-angular';
import { EventManagementPage } from '../event-management/event-management';
import { EventsProvider } from '../../providers/events/events'
import { FreelyEvent } from '../../models/freely-event';


/**
 * Generated class for the EventsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-events',
  templateUrl: 'events.html',
})
export class EventsPage {

  
  private eventList: Array<FreelyEvent>[];

  constructor(public eventsProvider: EventsProvider, private modalController: ModalController, public navCtrl: NavController, public navParams: NavParams) {
  }

  getItemImage(item){

  }

  private getEvents() {
    var organization = JSON.parse(localStorage.getItem("userData"));
    this.eventsProvider.getEventsOrganzation(organization.email).then(result => {
      if(result.status == "OK") {
        try {
            console.log("EVENTS req:");
            console.log(result.events);
            this.eventList = result.events;
            console.log("EVENTS:");
            console.log(this.eventList);
          } catch (error) {
            console.log("invalid event list");
          }
        }
      else{
        console.log("Invalid event data!");
      }
    });
 
  }

  ionViewDidLoad() {
    this.getEvents();
    console.log('ionViewDidLoad EventsPage');
  }

  openCreateEventModal(){
    let modal = this.modalController.create(CreateEventPage);
    modal.present();
  }

  goToEventDetails(event: any){
    this.navCtrl.setRoot(EventManagementPage, {event: event});
  }

}
