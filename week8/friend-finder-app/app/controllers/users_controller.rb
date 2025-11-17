class UsersController < ApplicationController
  before_action :require_login, only: [:show]

  def new
    @user = User.new
    redirect_to dashboard_path if logged_in?
  end

  def create
    @user = User.new(user_params)
    @user.email = @user.email.downcase
    @user.onboarded = false

    if @user.save
      session[:user_id] = @user.id
      redirect_to new_profile_path, notice: "Account created! Now let's set up your profile."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def show
    @user = User.find(params[:id])
    @profile = @user.profile
  end

  private

  def user_params
    params.require(:user).permit(:name, :email, :password, :password_confirmation, :age, :city)
  end
end
