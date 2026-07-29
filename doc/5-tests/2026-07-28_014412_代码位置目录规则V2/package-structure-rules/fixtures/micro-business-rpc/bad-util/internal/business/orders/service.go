package orders

import usersutil "example.com/app/internal/business/users/util"

func LoadUserProfile(requestJSON string) string {
	return usersutil.GetProfile(requestJSON)
}
