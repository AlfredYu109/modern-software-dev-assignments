class EventParticipant < ApplicationRecord
  belongs_to :event
  belongs_to :user

  validates :status, inclusion: { in: %w[interested confirmed declined] }
  validates :user_id, uniqueness: { scope: :event_id }

  scope :confirmed, -> { where(status: 'confirmed') }
end
