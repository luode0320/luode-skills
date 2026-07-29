package orders

import usersservice "example.com/app/internal/business/users/service"

func LoadUserProfile(requestJSON string) string {
	return usersservice.GetProfile(requestJSON)
}
