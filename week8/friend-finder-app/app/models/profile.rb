class Profile < ApplicationRecord
  belongs_to :user

  # Serialize arrays stored as text
  serialize :interests, type: Array, coder: JSON
  serialize :preferred_formats, type: Array, coder: JSON
  serialize :vibes, type: Array, coder: JSON

  validates :user, presence: true
end
