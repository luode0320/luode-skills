package orders

import usersrpc "example.com/app/internal/business/users/rpc"

func LoadUserProfile(requestJSON string) string {
	return usersrpc.GetProfile(requestJSON)
}
