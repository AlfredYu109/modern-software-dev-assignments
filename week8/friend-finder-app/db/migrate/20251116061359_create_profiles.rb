class CreateProfiles < ActiveRecord::Migration[7.2]
  def change
    create_table :profiles do |t|
      t.references :user, null: false, foreign_key: true
      t.string :hometown
      t.text :interests
      t.string :social_energy
      t.text :preferred_formats
      t.text :vibes
      t.text :routine
      t.text :transcript

      t.timestamps
    end
  end
end
