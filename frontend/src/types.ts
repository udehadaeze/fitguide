export type Metadata = {
  goals: string[]
  levels: string[]
  categories: string[]
  body_areas: string[]
  equipment: string[]
  locations: string[]
  intensities: string[]
  movement_restrictions: string[]
}

export type UserProfile = {
  goal: string
  fitness_level: string
  workout_location: string
  available_equipment: string[]
  preferred_duration_minutes: number
  preferred_intensity: string
  preferred_categories: string[]
  target_body_areas: string[]
  movement_restrictions: string[]
  exercises_to_avoid: string[]
  low_impact_required: boolean
  maximum_recommendations: number
}

export type Recommendation = {
  exercise_id: string
  name: string
  description: string
  category: string
  movement_pattern: string
  primary_body_area: string
  secondary_body_areas: string[]
  difficulty: string
  intensity: string
  equipment: string[]
  workout_locations: string[]
  estimated_duration_minutes: number
  recommended_repetitions: string
  recommended_sets: string
  beginner_friendly: boolean
  low_impact: boolean
  instructions: string
  safety_notes: string
  tags: string[]
  score: number
  matched_features: string[]
  explanation: string
  routine_position: number
  routine_role: string
}

export type RecommendationResponse = {
  processed_profile: {
    goal: string
    fitness_level: string
    workout_location: string
    preferred_duration_minutes: number
    preferred_intensity: string
    hard_restrictions_applied: string[]
  }
  recommendations: Recommendation[]
  eligible_count: number
  warning: string | null
}

