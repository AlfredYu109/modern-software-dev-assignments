class DashboardController < ApplicationController
  before_action :require_login
  before_action :require_onboarded, except: [:index]

  def index
    if !logged_in?
      redirect_to login_path
    elsif !current_user.onboarded
      redirect_to new_profile_path
    else
      @pending_matches = current_user.matches.pending.limit(3)
      @accepted_matches = current_user.matches.accepted.limit(5)
      @upcoming_events = Event.upcoming.limit(5)
      @friendship_score = calculate_friendship_score
    end
  end

  private

  def calculate_friendship_score
    # Friendship "garden" health score based on activity
    accepted = current_user.matches.accepted.count * 20
    recent_messages = current_user.messages.where('created_at > ?', 7.days.ago).count * 5
    events_attended = current_user.event_participants.count * 10

    [accepted + recent_messages + events_attended, 100].min
  end
end
