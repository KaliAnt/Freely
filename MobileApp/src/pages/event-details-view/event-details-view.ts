import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { FreelyEvent } from '../../models/freely-event';

/**
 * Generated class for the EventDetailsViewPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */


@Component({
  selector: 'page-event-details-view',
  templateUrl: 'event-details-view.html',
})
export class EventDetailsViewPage {
  eventObj:FreelyEvent;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.eventObj = navParams.get('item');
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EventDetailsViewPage');
  }

  getImagePicture() {
    return "assets/imgs/1.jpg";
  }

  onClickEvent(actionType: string) {

  }

}
