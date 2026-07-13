// 合规样例：order 业务只经 contract/user 接口调用 user 业务，不直连 business/user
package order

import (
	"example.com/app/internal/common"
	contractuser "example.com/app/internal/contract/user"
)

// Service 是 order 业务实现，依赖注入的跨业务接口
type Service struct {
	users contractuser.Reader
}

// Describe 通过 contract/user 接口获取用户名（依赖倒置，合规）
func (s *Service) Describe(id int64) string {
	_ = common.Version
	name, _ := s.users.GetName(id)
	return "order of " + name
}
