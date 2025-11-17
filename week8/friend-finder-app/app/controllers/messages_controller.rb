class MessagesController < ApplicationController
  before_action :require_login

  def create
    @match = Match.find(params[:match_id])
    @message = @match.messages.build(message_params)
    @message.sender = current_user

    if @message.save
      redirect_to match_path(@match), notice: "Message sent!"
    else
      redirect_to match_path(@match), alert: "Could not send message"
    end
  end

  private

  def message_params
    params.require(:message).permit(:content)
  end
end
