import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { FreelyEventData } from '../../models/freely-event-data';
import { FreelyEventApplicationView } from '../../models/freely-event-application-view';
import { FreelyOrganization} from '../../models/freely-organization'
import { StarRatingModule } from 'ionic3-star-rating';
import { Events } from 'ionic-angular';
import { FeedbackProvider } from '../../providers/feedback/feedback'

/**
 * Generated class for the FeedbackFormPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */


@Component({
  selector: 'page-feedback-form',
  templateUrl: 'feedback-form.html',
})
export class FeedbackFormPage {
  event: FreelyEventData;
  
  feedback: any = {
    rating: 4,
    description: "",
  }

  constructor(private feedbackProvider:FeedbackProvider, private events:Events, public navCtrl: NavController, public navParams: NavParams) {
    this.event = navParams.get('event');
    console.log("THIS IS THE EVENT:")
    console.log(this.event)
    events.subscribe('star-rating:changed', (starRating) => {this.feedback.rating = starRating;});
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad FeedbackFormPage');
  }

  submitBtn() {
    this.feedbackProvider.postFeedback(this.event.organization.email, "organization", this.feedback.rating, this.feedback.description).then(result => {
      if(result.status == "OK") {
        try {
            alert("Feedback submitted!")
            this.navCtrl.pop();
          } catch (error) {
            console.log("invalid applications list");
          }
        }
      else{
        console.log("Invalid event data!");
      }
    });
  }

}
