class Match < ApplicationRecord
  belongs_to :user
  belongs_to :matched_user, class_name: 'User'

  has_many :messages, dependent: :destroy

  validates :status, inclusion: { in: %w[pending accepted rejected] }
  validates :compatibility_score, numericality: { greater_than_or_equal_to: 0, less_than_or_equal_to: 100 }, allow_nil: true

  scope :accepted, -> { where(status: 'accepted') }
  scope :pending, -> { where(status: 'pending') }

  def update_last_contact!
    update(last_contact: Time.current)
  end
end
