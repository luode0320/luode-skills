package orders

import usersentity "example.com/app/internal/business/users/entity"

func LoadUserProfile(requestJSON string) string {
	return usersentity.GetProfile(requestJSON)
}
