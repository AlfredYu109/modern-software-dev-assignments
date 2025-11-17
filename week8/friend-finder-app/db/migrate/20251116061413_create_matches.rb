class CreateMatches < ActiveRecord::Migration[7.2]
  def change
    create_table :matches do |t|
      t.references :user, null: false, foreign_key: true
      t.references :matched_user, null: false, foreign_key: { to_table: :users }
      t.float :compatibility_score
      t.string :status
      t.datetime :last_contact

      t.timestamps
    end

    add_index :matches, [:user_id, :matched_user_id], unique: true
  end
end
