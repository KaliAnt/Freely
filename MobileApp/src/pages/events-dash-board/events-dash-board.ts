import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { EventDetailsViewPage } from '../event-details-view/event-details-view'
import { EventsProvider } from '../../providers/events/events';
import { Slides } from 'ionic-angular';
import { ViewChild } from '@angular/core';
import { FreelyEvent } from '../../models/freely-event'
import { EventListener } from '@angular/core/src/debug/debug_node';
import { templateJitUrl, removeSummaryDuplicates } from '@angular/compiler';
import { Events } from 'ionic-angular';
/**
 * Generated class for the EventsDashBoardPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-events-dash-board',
  templateUrl: 'events-dash-board.html',
})
export class EventsDashBoardPage {

  @ViewChild(Slides) slides: Slides;
  private eventsList: Array<FreelyEvent>;
  // @ViewChild(Slides) slides: Slides;
  // private eventsList: Array<any> = [ {
  //   name: "DreamArt Festival",
  //   description: "Dreaming",
  //   date: "12 Dec 2018"
  // },
  // {
  //   name: "Spooky Party",
  //   description: "Spooky",
  //   date: "28 Nov 2018"
  // },
  // {
  //   name: "Feel The Real Festival",
  //   description: "Real",
  //   date: "02 Ian 2019"
  // }];
  
  private currentEvent: FreelyEvent = {
    name: "Dream festival",
    description: "test",
    date: "4 - 7 nov 2018",
    organizer: "ORGANIZER",
    location: "",
    organizerEmail: ""
  };

  constructor(private ev: Events, public eventsProvider: EventsProvider, public navCtrl: NavController, public navParams: NavParams) {
   
  }

  private getEvents() {
    this.eventsProvider.getEvents().then(result => {
      if(result.status == "OK") {
        try {
            this.eventsList = result.events;
          } catch (error) {
            console.log("invalid event list");
          }
        }
      else{
        console.log("Invalid event data!");
      }
    });
  }


  getImagePicture(item){
      return "assets/imgs/1.jpg";
  }

  onClickEvent(type: string){
    if(type == "decline"){

    }else if(type == "apply"){

    }else{

    }

    var current = this.slides.getActiveIndex();
    this.slides.slideTo(current - 1, 500);
  }

  showEvent(item: any) {
    this.navCtrl.push(EventDetailsViewPage,{item:item});
  }

  onInput(ev) {
    console.log("USER INPUT:")
    console.log(ev)
  }

  onCancel(ev) {
    console.log("USER CANCEL:")
    console.log(ev)
  }

  ionViewDidLoad() {
    this.getEvents();
    // this.eventsProvider.getEvents().then(data=>{
    //    this.eventsList = data;
    //    this.currentEvent = this.eventsList[0];
    //  });
  }

}
