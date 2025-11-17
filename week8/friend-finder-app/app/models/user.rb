class User < ApplicationRecord
  has_secure_password

  has_one :profile, dependent: :destroy
  has_many :matches, dependent: :destroy
  has_many :matched_users, through: :matches
  has_many :messages, foreign_key: :sender_id, dependent: :destroy
  has_many :created_events, class_name: 'Event', foreign_key: :created_by_id, dependent: :destroy
  has_many :event_participants, dependent: :destroy
  has_many :events, through: :event_participants

  validates :email, presence: true, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, presence: true
  validates :age, numericality: { only_integer: true, greater_than_or_equal_to: 21, less_than_or_equal_to: 26 }, allow_nil: true
end
