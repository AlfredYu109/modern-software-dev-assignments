class Event < ApplicationRecord
  belongs_to :created_by, class_name: 'User'

  has_many :event_participants, dependent: :destroy
  has_many :participants, through: :event_participants, source: :user

  validates :title, presence: true
  validates :event_date, presence: true
  validates :max_participants, numericality: { only_integer: true, greater_than: 0 }, allow_nil: true

  scope :upcoming, -> { where('event_date > ?', Time.current).order(:event_date) }
  scope :by_category, ->(category) { where(category: category) }

  def full?
    max_participants.present? && participants.count >= max_participants
  end

  def available_spots
    return nil unless max_participants
    max_participants - participants.count
  end
end
