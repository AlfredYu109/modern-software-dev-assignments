class Message < ApplicationRecord
  belongs_to :match
  belongs_to :sender, class_name: 'User'

  validates :content, presence: true

  after_create :update_match_last_contact

  scope :unread, -> { where(read: false) }

  private

  def update_match_last_contact
    match.update_last_contact!
  end
end
