// 违规样例中的 user 业务本身合规，仅被 order 非法直连
package user

// Service 是 user 业务实现
type Service struct{}

// GetName 返回用户名
func (s *Service) GetName(id int64) (string, error) {
	return "alice", nil
}
