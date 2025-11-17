class MatchesController < ApplicationController
  before_action :require_login
  before_action :require_onboarded

  def index
    @pending_matches = current_user.matches.pending.includes(:matched_user)
    @accepted_matches = current_user.matches.accepted.includes(:matched_user)
  end

  def show
    @match = current_user.matches.find(params[:id])
    @messages = @match.messages.order(created_at: :asc)
    @new_message = Message.new
  end

  def create
    # Manual match creation (if needed)
    matched_user = User.find(params[:matched_user_id])
    @match = current_user.matches.build(
      matched_user: matched_user,
      status: 'pending',
      compatibility_score: calculate_compatibility(current_user, matched_user)
    )

    if @match.save
      redirect_to matches_path, notice: "Match request sent!"
    else
      redirect_to matches_path, alert: "Could not create match"
    end
  end

  def accept
    @match = current_user.matches.find(params[:id])
    @match.update(status: 'accepted')
    redirect_to matches_path, notice: "Match accepted!"
  end

  def reject
    @match = current_user.matches.find(params[:id])
    @match.update(status: 'rejected')
    redirect_to matches_path, notice: "Match declined"
  end

  def generate
    # Generate AI-powered matches based on compatibility
    potential_matches = find_potential_matches(current_user)

    potential_matches.each do |user|
      next if Match.exists?(user_id: current_user.id, matched_user_id: user.id)

      Match.create(
        user: current_user,
        matched_user: user,
        status: 'pending',
        compatibility_score: calculate_compatibility(current_user, user)
      )
    end

    redirect_to matches_path, notice: "New matches generated!"
  end

  private

  def find_potential_matches(user)
    return [] unless user.profile

    # Find users with similar interests, age, and city
    User.joins(:profile)
        .where.not(id: user.id)
        .where(city: user.city)
        .where(onboarded: true)
        .where.not(id: user.matches.pluck(:matched_user_id))
        .limit(5)
  end

  def calculate_compatibility(user1, user2)
    return 0 unless user1.profile && user2.profile

    score = 0

    # Interest overlap
    common_interests = (user1.profile.interests & user2.profile.interests).size
    score += common_interests * 20

    # Social energy match
    score += 20 if user1.profile.social_energy == user2.profile.social_energy

    # Same city
    score += 15 if user1.city == user2.city

    # Vibe overlap
    common_vibes = (user1.profile.vibes & user2.profile.vibes).size
    score += common_vibes * 15

    [score, 100].min # Cap at 100
  end
end
