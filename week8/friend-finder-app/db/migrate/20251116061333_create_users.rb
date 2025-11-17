class CreateUsers < ActiveRecord::Migration[7.2]
  def change
    create_table :users do |t|
      t.string :email
      t.string :password_digest
      t.string :name
      t.integer :age
      t.string :city
      t.boolean :onboarded

      t.timestamps
    end
  end
end
