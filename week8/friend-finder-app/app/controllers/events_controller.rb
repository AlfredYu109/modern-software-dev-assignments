class EventsController < ApplicationController
  before_action :require_login
  before_action :require_onboarded
  before_action :set_event, only: [:show, :join, :leave]

  def index
    @events = Event.upcoming.includes(:participants, :created_by)
  end

  def show
    @participants = @event.participants
  end

  def new
    @event = Event.new
  end

  def create
    @event = current_user.created_events.build(event_params)

    if @event.save
      @event.participants << current_user
      redirect_to events_path, notice: "Event created successfully!"
    else
      render :new, status: :unprocessable_entity
    end
  end

  def join
    if @event.full?
      redirect_to event_path(@event), alert: "Event is full!"
    else
      EventParticipant.create(event: @event, user: current_user, status: 'interested')
      redirect_to event_path(@event), notice: "You've joined the event!"
    end
  end

  def leave
    participation = EventParticipant.find_by(event: @event, user: current_user)
    participation&.destroy
    redirect_to events_path, notice: "You've left the event"
  end

  private

  def set_event
    @event = Event.find(params[:id])
  end

  def event_params
    params.require(:event).permit(:title, :description, :location, :event_date, :max_participants, :category)
  end
end
