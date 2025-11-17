class ProfilesController < ApplicationController
  before_action :require_login
  before_action :set_profile, only: [:edit, :update]

  def new
    if current_user.profile.present?
      redirect_to dashboard_path, notice: "Profile already exists"
    else
      @profile = current_user.build_profile
    end
  end

  def create
    @profile = current_user.build_profile(profile_params)

    if @profile.save
      current_user.update(onboarded: true)
      redirect_to dashboard_path, notice: "Profile created successfully!"
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
    redirect_to new_profile_path unless @profile
  end

  def update
    if @profile.update(profile_params)
      current_user.update(onboarded: true)
      redirect_to dashboard_path, notice: "Profile updated successfully!"
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def process_voice
    transcript = params[:transcript]

    # Simulate AI processing (in production, this would call OpenAI API)
    processed_data = simulate_ai_processing(transcript)

    render json: { success: true, data: processed_data }
  rescue => e
    render json: { success: false, error: e.message }, status: :unprocessable_entity
  end

  private

  def set_profile
    @profile = current_user.profile
  end

  def profile_params
    permitted = params.require(:profile).permit(:hometown, :social_energy, :routine, :transcript, :interests, :preferred_formats, :vibes)

    # Convert comma-separated strings to arrays
    [:interests, :preferred_formats, :vibes].each do |field|
      if permitted[field].is_a?(String)
        permitted[field] = permitted[field].split(',').map(&:strip).reject(&:blank?)
      end
    end

    permitted
  end

  def simulate_ai_processing(transcript)
    # Simulated AI analysis - in production, use OpenAI API
    interests = ["coffee", "hiking", "board games", "concerts"]
    vibes = ["chill outdoorsy", "creative", "social"]
    preferred_formats = ["1-on-1 coffee", "small group hangouts"]

    {
      interests: interests.sample(2),
      vibes: vibes.sample(2),
      preferred_formats: preferred_formats.sample(1),
      social_energy: ["introvert", "ambivert", "extrovert"].sample,
      routine: "Likes weekend activities and evening hangouts"
    }
  end
end
