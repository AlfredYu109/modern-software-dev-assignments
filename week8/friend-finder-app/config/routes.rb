Rails.application.routes.draw do
  root "dashboard#index"

  # Authentication
  get "login", to: "sessions#new"
  post "login", to: "sessions#create"
  delete "logout", to: "sessions#destroy"
  get "signup", to: "users#new"
  post "signup", to: "users#create"

  # Resources
  resources :users, only: [:show]
  resources :profiles, only: [:new, :create, :edit, :update]
  resources :matches, only: [:index, :show, :create] do
    member do
      patch :accept
      patch :reject
    end
    resources :messages, only: [:create]
  end
  resources :events do
    member do
      post :join
      delete :leave
    end
  end

  # Dashboard
  get "dashboard", to: "dashboard#index"

  # API endpoints for voice processing
  post "api/process_voice", to: "profiles#process_voice"
  post "api/generate_matches", to: "matches#generate"

  # Health check
  get "up" => "rails/health#show", as: :rails_health_check

  # PWA
  get "service-worker" => "rails/pwa#service_worker", as: :pwa_service_worker
  get "manifest" => "rails/pwa#manifest", as: :pwa_manifest
end
