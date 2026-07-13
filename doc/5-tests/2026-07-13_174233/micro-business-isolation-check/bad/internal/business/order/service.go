// 违规样例：order 业务直接 import business/user 内部路径（破坏横向零依赖）
package order

import (
	userbiz "example.com/app/internal/business/user"
)

// Service 直接持有 user 业务的具体实现（违规：应改走 contract/user 接口）
type Service struct {
	users *userbiz.Service
}

// Describe 直连 business/user 调用（违规）
func (s *Service) Describe(id int64) string {
	name, _ := s.users.GetName(id)
	return "order of " + name
}
