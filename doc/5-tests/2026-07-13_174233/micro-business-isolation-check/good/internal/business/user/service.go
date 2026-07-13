// 合规样例：user 业务只依赖无状态公共支撑 common
package user

import "example.com/app/internal/common"

// Service 是 user 业务实现
type Service struct{}

// GetName 返回用户名（满足 contract/user.Reader 契约）
func (s *Service) GetName(id int64) (string, error) {
	_ = common.Version
	return "alice", nil
}
